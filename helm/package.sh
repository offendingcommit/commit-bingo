#!/bin/bash
# Script to package and optionally deploy the Helm chart

set -e

# Default values
DIST_DIR="../dist"
CHART_DIR="bingo"
CHART_VERSION=$(grep 'version:' ${CHART_DIR}/Chart.yaml | awk '{print $2}')
RELEASE_NAME="bingo"
NAMESPACE="default"
DEPLOY=false

# Display help
function show_help {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -d, --deploy         Deploy the chart after packaging"
  echo "  -n, --namespace      Kubernetes namespace (default: default)"
  echo "  -r, --release        Release name (default: bingo)"
  echo "  -h, --help           Show this help message"
  echo ""
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
  -d | --deploy)
    DEPLOY=true
    shift
    ;;
  -n | --namespace)
    NAMESPACE="$2"
    shift
    shift
    ;;
  -r | --release)
    RELEASE_NAME="$2"
    shift
    shift
    ;;
  -h | --help)
    show_help
    exit 0
    ;;
  *)
    echo "Unknown option: $1"
    show_help
    exit 1
    ;;
  esac
done

echo "Packaging Helm chart ${CHART_DIR} version ${CHART_VERSION}..."
helm package ${CHART_DIR} --destination ${DIST_DIR}

if [ "$DEPLOY" = true ]; then
  echo "Deploying chart to Kubernetes namespace ${NAMESPACE} with release name ${RELEASE_NAME}..."
  helm upgrade --install ${RELEASE_NAME} ${DIST_DIR}/${CHART_DIR}-${CHART_VERSION}.tgz --namespace ${NAMESPACE} --create-namespace

  echo "Deployment complete. You can access the application using:"
  echo "kubectl port-forward -n ${NAMESPACE} svc/${RELEASE_NAME} 8080:8080"
else
  echo "Chart packaged successfully. To deploy, run:"
  echo "helm install ${RELEASE_NAME} ${DIST_DIR}/${CHART_DIR}-${CHART_VERSION}.tgz --namespace ${NAMESPACE} --create-namespace"
fi
