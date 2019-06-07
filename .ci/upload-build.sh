#!/usr/bin/env bash
# Pilfered from https://cirrus-ci.org/examples/#release-assets
set -euo pipefail

if ! [[ -v CIRRUS_RELEASE ]]; then
	echo "Not a release. No need to deploy!"
	exit 0
fi

REQUIRED_VARS=( GITHUB_TOKEN TWINE_{REPOSITORY_URL,USER,PASSWORD} )
for var in "${REQUIRED_VARS[@]}"; do
	if ! [[ -v "$var" ]]; then
		echo "Please set environment variable '$var' !"
		exit 1
	fi
done


file_content_type="application/octet-stream"
files_to_upload=( dist/* )

for fpath in "${files_to_upload[@]}"; do
	echo "Uploading '$fpath' to Github..."
	name=$(basename "$fpath")
	url_to_upload="https://uploads.github.com/repos/$CIRRUS_REPO_FULL_NAME/releases/$CIRRUS_RELEASE/assets?name=$name"
	curl -i -X POST \
		--data-binary @$fpath \
		--header "Authorization: token $GITHUB_TOKEN" \
		--header "Content-Type: $file_content_type" \
		$url_to_upload
done

twine upload \
	--repository-url "$TWINE_REPOSITORY_URL" \
	--username "$TWINE_USER" \
	--password "$TWINE_PASSWORD" \
	"${files_to_upload[@]}"
