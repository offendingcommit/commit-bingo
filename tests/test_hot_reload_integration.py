"""
Integration test for hot reload persistence using Playwright.
This test verifies that game state persists when the app is reloaded.
"""

import asyncio
import json
from pathlib import Path

import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.e2e
@pytest.mark.playwright
@pytest.mark.slow
@pytest.mark.persistence
@pytest.mark.requires_app
class TestHotReloadIntegration:
    """Integration tests for hot reload state persistence."""
    
    @pytest.mark.asyncio
    async def test_state_persists_on_page_reload(self):
            """Test that game state persists when page is reloaded."""
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                try:
                    # Navigate to the app
                    await page.goto("http://localhost:8080")
                    await page.wait_for_load_state("networkidle")
                    
                    # Get all clickable tiles
                    tiles = await page.locator("[style*='cursor: pointer']").all()
                    assert len(tiles) == 25, f"Should have exactly 25 tiles, got {len(tiles)}"
                    
                    # Click tiles by position (avoiding FREE MEAT at position 12)
                    # Map positions to board coordinates for verification
                    tiles_to_click = [
                        0,   # (0,0) - top-left
                        4,   # (0,4) - top-right
                        6,   # (1,1) - second row, second col
                    ]
                    
                    for tile_index in tiles_to_click:
                        await tiles[tile_index].click()
                        await asyncio.sleep(0.2)  # Wait for state save
                    
                    # Take screenshot before reload
                    await page.screenshot(path="before_reload.png")
                    
                    # Check state file exists and has correct data
                    state_file = Path("game_state.json")
                    assert state_file.exists(), "State file should exist"
                    
                    with open(state_file, 'r') as f:
                        state = json.load(f)
                    
                    # Verify clicked tiles are saved (our 3 clicks + FREE MEAT)
                    assert len(state['clicked_tiles']) == 4, f"Should have 4 clicked tiles, got {len(state['clicked_tiles'])}"
                    
                    # Store clicked positions for verification
                    clicked_positions = set(tuple(pos) for pos in state['clicked_tiles'])
                    
                    # Reload the page
                    await page.reload()
                    await page.wait_for_load_state("networkidle")
                    
                    # Take screenshot after reload
                    await page.screenshot(path="after_reload.png")
                    
                    # Verify the board is restored
                    restored_tiles = await page.locator("[style*='cursor: pointer']").all()
                    assert len(restored_tiles) == 25, f"Should still have 25 tiles after reload, got {len(restored_tiles)}"
                    
                    # Read state file again to verify it still has the same data
                    with open(state_file, 'r') as f:
                        restored_state = json.load(f)
                    
                    restored_positions = set(tuple(pos) for pos in restored_state['clicked_tiles'])
                    assert clicked_positions == restored_positions, "Clicked tiles should be preserved"
                    
                    # Verify we have the expected number of tiles clicked
                    assert len(restored_positions) == 4, f"Should have exactly 4 clicked tiles after reload, got {len(restored_positions)}"
                    
                finally:
                    await browser.close()

    
    @pytest.mark.asyncio
    async def test_state_persists_across_sessions(self):
        """Test that state persists across different browser sessions."""
        async with async_playwright() as p:
            # First session - create some state
            browser1 = await p.chromium.launch(headless=True)
            page1 = await browser1.new_page()
            
            try:
                await page1.goto("http://localhost:8080")
                await page1.wait_for_load_state("networkidle")
                
                # Click a specific pattern
                tiles = ["THREATEN GOOD TIME", "THAT'S NOICE", "MAKES AIR QUOTES"]
                for tile in tiles:
                    await page1.locator(f"text={tile}").first.click()
                    await asyncio.sleep(0.1)
                
                # Close first browser
                await browser1.close()
                
                # Wait a bit for state to be saved
                await asyncio.sleep(0.5)
                
                # Second session - verify state is loaded
                browser2 = await p.chromium.launch(headless=True)
                page2 = await browser2.new_page()
                
                await page2.goto("http://localhost:8080")
                await page2.wait_for_load_state("networkidle")
                
                # Verify the state file has the expected data
                state_file = Path("game_state.json")
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                # Should have at least our 3 clicks plus FREE MEAT
                assert len(state['clicked_tiles']) >= 4
                
                await browser2.close()
                
            except Exception as e:
                if 'browser1' in locals():
                    await browser1.close()
                if 'browser2' in locals():
                    await browser2.close()
                raise e
    
    @pytest.mark.asyncio
    async def test_concurrent_users_see_same_state(self):
        """Test that multiple concurrent users see the same game state."""
        async with async_playwright() as p:
            # Launch two browsers
            browser1 = await p.chromium.launch(headless=True)
            browser2 = await p.chromium.launch(headless=True)
            
            page1 = await browser1.new_page()
            page2 = await browser2.new_page()
            
            try:
                # Both users navigate to the app
                await page1.goto("http://localhost:8080")
                await page2.goto("http://localhost:8080")
                
                await page1.wait_for_load_state("networkidle")
                await page2.wait_for_load_state("networkidle")
                
                # User 1 clicks a tile
                await page1.locator("text=SAYS KUBERNETES").first.click()
                await asyncio.sleep(0.2)  # Wait for state save and sync
                
                # User 2 reloads to get updated state
                await page2.reload()
                await page2.wait_for_load_state("networkidle")
                
                # Both should see the same state file
                state_file = Path("game_state.json")
                with open(state_file, 'r') as f:
                    state = json.load(f)
                
                # Verify the clicked tile is in the state
                clicked_positions = [tuple(pos) for pos in state['clicked_tiles']]
                assert (0, 4) in clicked_positions, "SAYS KUBERNETES (0,4) should be clicked"
                
                # User 2 clicks another tile
                await page2.locator("text=POSITION ONE").first.click()
                await asyncio.sleep(0.2)
                
                # User 1 reloads
                await page1.reload()
                await page1.wait_for_load_state("networkidle")
                
                # Verify both clicks are saved
                with open(state_file, 'r') as f:
                    final_state = json.load(f)
                
                final_positions = [tuple(pos) for pos in final_state['clicked_tiles']]
                assert (0, 4) in final_positions, "First user's click should be saved"
                assert (4, 4) in final_positions, "Second user's click should be saved"
                
            finally:
                await browser1.close()
                await browser2.close()


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])