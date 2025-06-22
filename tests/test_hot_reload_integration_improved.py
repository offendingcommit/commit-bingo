"""
Improved integration test for hot reload persistence.
This test focuses on validating the core state persistence mechanism
without depending on specific board content.
"""

import asyncio
import json
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect


class TestHotReloadIntegrationImproved:
    """Integration tests for hot reload state persistence."""
    
    @pytest.mark.asyncio
    async def test_state_persistence_mechanism(self):
        """Test that the state persistence mechanism works correctly."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Navigate to the app
                await page.goto("http://localhost:8080")
                await page.wait_for_load_state("networkidle")
                
                # Verify board is loaded
                tiles = await page.locator("[style*='cursor: pointer']").all()
                assert len(tiles) == 25, f"Should have exactly 25 tiles, got {len(tiles)}"
                
                # Map tile indices to board positions
                # Board is 5x5, so index = row * 5 + col
                tiles_to_click = [
                    (0, 0),  # Top-left
                    (0, 4),  # Top-right
                    (1, 1),  # Second row, second column
                    (3, 2),  # Fourth row, middle
                ]
                
                # Click tiles by their board position
                for row, col in tiles_to_click:
                    index = row * 5 + col
                    await tiles[index].click()
                    await asyncio.sleep(0.1)  # Small delay for state save
                
                # Wait a bit longer to ensure all saves complete
                await asyncio.sleep(0.5)
                
                # Verify state file exists and contains our clicks
                state_file = Path("game_state.json")
                assert state_file.exists(), "State file should exist"
                
                with open(state_file, 'r') as f:
                    state_before = json.load(f)
                
                # Convert to set of tuples for easier comparison
                clicked_before = {tuple(pos) for pos in state_before['clicked_tiles']}
                
                # Should have our 4 clicks + FREE MEAT at (2,2)
                assert len(clicked_before) == 5, f"Should have 5 clicked tiles, got {len(clicked_before)}"
                
                # Verify our clicked positions are in the state
                for pos in tiles_to_click:
                    assert pos in clicked_before, f"Position {pos} should be in clicked tiles"
                
                # Verify FREE MEAT is clicked
                assert (2, 2) in clicked_before, "FREE MEAT at (2,2) should be clicked"
                
                # Take screenshot before reload for debugging
                await page.screenshot(path="test_before_reload.png")
                
                # Reload the page
                await page.reload()
                await page.wait_for_load_state("networkidle")
                
                # Take screenshot after reload for debugging
                await page.screenshot(path="test_after_reload.png")
                
                # Verify state file still exists and has same data
                with open(state_file, 'r') as f:
                    state_after = json.load(f)
                
                clicked_after = {tuple(pos) for pos in state_after['clicked_tiles']}
                
                # State should be identical
                assert clicked_before == clicked_after, "Clicked tiles should be preserved after reload"
                
                # Verify board hasn't changed
                assert state_before['board'] == state_after['board'], "Board should remain the same"
                assert state_before['board_iteration'] == state_after['board_iteration'], "Board iteration should remain the same"
                assert state_before['today_seed'] == state_after['today_seed'], "Seed should remain the same"
                
            finally:
                await browser.close()
    
    @pytest.mark.asyncio
    async def test_visual_state_restoration(self):
        """Test that clicked tiles visually appear clicked after reload."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Set to True for CI
            page = await browser.new_page()
            
            try:
                # Navigate to the app
                await page.goto("http://localhost:8080")
                await page.wait_for_load_state("networkidle")
                
                # Click a specific tile and get its visual state
                first_tile = page.locator("[style*='cursor: pointer']").first
                
                # Get background color before clicking
                bg_before = await first_tile.evaluate("el => window.getComputedStyle(el).backgroundColor")
                
                # Click the tile
                await first_tile.click()
                await asyncio.sleep(0.5)
                
                # Get background color after clicking
                bg_after_click = await first_tile.evaluate("el => window.getComputedStyle(el).backgroundColor")
                
                # Colors should be different (tile is now clicked)
                assert bg_before != bg_after_click, "Tile background should change when clicked"
                
                # Reload the page
                await page.reload()
                await page.wait_for_load_state("networkidle")
                
                # Get the same tile after reload
                first_tile_after_reload = page.locator("[style*='cursor: pointer']").first
                
                # Get background color after reload
                bg_after_reload = await first_tile_after_reload.evaluate("el => window.getComputedStyle(el).backgroundColor")
                
                # Color should match the clicked state
                assert bg_after_click == bg_after_reload, "Tile should maintain clicked appearance after reload"
                
            finally:
                await browser.close()
    
    @pytest.mark.asyncio
    async def test_multiple_sessions_share_state(self):
        """Test that multiple browser sessions see the same state."""
        async with async_playwright() as p:
            browser1 = await p.chromium.launch(headless=True)
            browser2 = await p.chromium.launch(headless=True)
            
            try:
                # User 1 connects
                page1 = await browser1.new_page()
                await page1.goto("http://localhost:8080")
                await page1.wait_for_load_state("networkidle")
                
                # User 1 clicks a tile
                tiles1 = await page1.locator("[style*='cursor: pointer']").all()
                await tiles1[0].click()  # Click first tile
                await asyncio.sleep(0.5)
                
                # User 2 connects
                page2 = await browser2.new_page()
                await page2.goto("http://localhost:8080")
                await page2.wait_for_load_state("networkidle")
                
                # Both users should see the same state
                state_file = Path("game_state.json")
                with open(state_file, 'r') as f:
                    shared_state = json.load(f)
                
                clicked_tiles = {tuple(pos) for pos in shared_state['clicked_tiles']}
                
                # Should have tile at (0,0) and FREE MEAT at (2,2)
                assert (0, 0) in clicked_tiles, "First tile should be clicked"
                assert (2, 2) in clicked_tiles, "FREE MEAT should be clicked"
                assert len(clicked_tiles) == 2, "Should have exactly 2 clicked tiles"
                
                # User 2 clicks another tile
                tiles2 = await page2.locator("[style*='cursor: pointer']").all()
                await tiles2[6].click()  # Click a different tile
                await asyncio.sleep(0.5)
                
                # User 1 reloads to see User 2's changes
                await page1.reload()
                await page1.wait_for_load_state("networkidle")
                
                # Check final state
                with open(state_file, 'r') as f:
                    final_state = json.load(f)
                
                final_clicked = {tuple(pos) for pos in final_state['clicked_tiles']}
                assert len(final_clicked) == 3, "Should have 3 clicked tiles after both users clicked"
                
            finally:
                await browser1.close()
                await browser2.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])