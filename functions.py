def search_song(title, artist, limit):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_ID,
                                                           client_secret=client_secret))
    try:
        results = sp.search(q=f"{title} {artist}", type='track', limit=limit)
        song_id = results['tracks']['items'][0]['id']
        return song_id
    except IndexError:
        print("Song not found!")
        return ""

def get_audio_features(list_of_song_ids):

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_ID,
                                                           client_secret=client_secret))

    audio_features_dict = {'id': [], 'danceability': [], 'energy': [],
                           'key': [], 'loudness': [], 'mode': [],
                           'speechiness': [], 'acousticness': [],
                           'instrumentalness': [], 'liveness': [],
                           'valence': [], 'tempo': []}
  
    chunks = np.array_split(list_of_song_ids, len(list_of_song_ids) // 50 + 1)

    for chunk in chunks:
        print("Collecting IDs for chunk...")
        time.sleep(20) 
        features = sp.audio_features(chunk)
        for feature in features:
            for key, value in feature.items():
                if key in audio_features_dict:
                    audio_features_dict[key].append(value)

    audio_features_df = pd.DataFrame(audio_features_dict)
    return audio_features_df

def add_audio_features(df, audio_features_df):
  
    merged_df = pd.merge(df, audio_features_df, on='id', how='inner')
    return merged_df