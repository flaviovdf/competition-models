#!/bin/bash

TABLES=(twitter_movie twitter_genre youtube_ufmg lastfm_artist \
    mmusic_artist brightkite_locs twitter_hashtag)

for table in ${TABLES[@]}; do
    ./pyrun.sh scripts/pdf_cdf_ccdf.py $table
    ./pyrun.sh scripts/plot_inter_arrival.py $table user
    ./pyrun.sh scripts/plot_inter_arrival.py $table obj
    ./pyrun.sh scripts/plot_inter_arrival.py $table pair
    ./pyrun.sh scripts/variety.py $table
    #./pyrun.sh scripts/plot_user_series.py $table 
done
