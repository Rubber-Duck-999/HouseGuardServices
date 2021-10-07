#!/bin/sh

run()
{
	SRC=/home/simon/Downloads/$1
	doctor="Doctor-Who-1963"
	DEST=/media/newdrive/Plex_Archive/Tv_Shows/$doctor/$2/
	DEST_EXT=mp4
	HANDBRAKE_CLI=HandBrakeCLI
	for FILE in `ls $SRC`
	do
		filename=$(basename $FILE)
		extension=${filename##*.}
		filename=${filename%.*}

		$HANDBRAKE_CLI -i $SRC/$FILE -o $DEST/$filename.$DEST_EXT -Z 'General/Very Fast 1080p30'
	done
}

run season-22 Season-22
run season-23 Season-23
