"""
Provides movie recommendation algorithms and functionality
"""
import pandas as pd
import numpy as np
from data_handler import DataHandler
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

class MovieRecommender:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.similarity_matrix = None
        self.movie_indices = {}
        self.feature_matrix = None
        self._initialize_recommendation_matrices()
        
    def _initialize_recommendation_matrices(self):
        """Initialize matrices for content-based recommendations"""
        try:
            # Get the dataframe from data handler
            df = self.data_handler.df
            
            if df is None or len(df) == 0:
                print("Warning: Empty dataset, can't initialize recommendation matrices")
                return
                
            # Create a feature matrix using genres, keywords, and cast
            features = []
            
            # Check which features are available
            has_genres = 'genres_list' in df.columns
            has_keywords = 'keywords_list' in df.columns
            has_cast = 'cast_list' in df.columns
            has_director = 'director' in df.columns
            
            # Skip if no useful features are available
            if not (has_genres or has_keywords or has_cast or has_director):
                print("Warning: No useful features for recommendations")
                return
                
            # Process each movie to extract features
            for _, row in df.iterrows():
                movie_features = []
                
                # Add genres (weight: 3)
                if has_genres and isinstance(row.get('genres_list'), list):
                    movie_features.extend([f"genre_{g.lower().replace(' ', '_')}" for g in row['genres_list']] * 3)
                    
                # Add keywords (weight: 1)
                if has_keywords and isinstance(row.get('keywords_list'), list):
                    movie_features.extend([f"kw_{k.lower().replace(' ', '_')}" for k in row['keywords_list']])
                    
                # Add top cast members (weight: 2)
                if has_cast and isinstance(row.get('cast_list'), list):
                    # Use only top cast members to reduce dimensionality
                    top_cast = row['cast_list'][:3] if len(row['cast_list']) > 3 else row['cast_list']
                    movie_features.extend([f"actor_{a.lower().replace(' ', '_')}" for a in top_cast] * 2)
                    
                # Add director (weight: 3)
                if has_director and row.get('director'):
                    movie_features.extend([f"director_{row['director'].lower().replace(' ', '_')}"] * 3)
                    
                features.append(movie_features)
                
            # Convert features to a count-based representation
            feature_counter = [Counter(f) for f in features]
            all_features = set()
            for counter in feature_counter:
                all_features.update(counter.keys())
                
            # Create a mapping of movies to indices for fast lookup
            self.movie_indices = {int(movie_id): idx for idx, movie_id in enumerate(df['id'])}
            
            # Create the sparse feature matrix (movies × features)
            self.feature_matrix = np.zeros((len(df), len(all_features)))
            feature_to_idx = {feature: idx for idx, feature in enumerate(all_features)}
            
            for i, counter in enumerate(feature_counter):
                for feature, count in counter.items():
                    self.feature_matrix[i, feature_to_idx[feature]] = count
                    
            # Calculate similarity matrix
            self.similarity_matrix = cosine_similarity(self.feature_matrix)
            
            print(f"Initialized recommendation matrices for {len(df)} movies")
        except Exception as e:
            print(f"Error initializing recommendation matrices: {e}")
            # Create empty matrices to prevent app crashes
            self.similarity_matrix = None
            self.movie_indices = {}
    
    def get_popular_recommendations(self, limit=10):
        """Get recommendations based on popularity"""
        return self.data_handler.get_popular_movies(limit)
    
    def get_trending_recommendations(self, limit=10):
        """Get recommendations based on trending status"""
        return self.data_handler.get_trending_movies(limit)
    
    def get_similar_movies(self, movie_id, limit=10):
        """Get recommendations based on similarity to a specific movie"""
        # Try the improved content-based approach first
        improved_recommendations = self.get_similar_movies_improved(movie_id, limit)
        
        # Fall back to the basic approach if needed
        if improved_recommendations:
            return improved_recommendations
        return self.data_handler.get_movie_recommendations(movie_id, limit)
    
    def get_similar_movies_improved(self, movie_id, limit=20):
        """
        Enhanced recommendation method using pre-computed similarity matrix
        
        Parameters:
        - movie_id: ID of the movie to find similar movies for
        - limit: Maximum number of recommendations to return
        
        Returns:
        - List of recommended movies or empty list if similarity matrix isn't available
        """
        try:
            if self.similarity_matrix is None or not self.movie_indices:
                return []
                
            # Convert movie_id to int if it's not already
            movie_id = int(movie_id)
            
            # Get the movie index in our matrix
            if movie_id not in self.movie_indices:
                return []
                
            movie_idx = self.movie_indices[movie_id]
            
            # Get similarity scores for this movie with all others
            sim_scores = list(enumerate(self.similarity_matrix[movie_idx]))
            
            # Sort movies by similarity score
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Get the most similar movies (excluding itself)
            sim_scores = [x for x in sim_scores if x[0] != movie_idx][:limit]
            
            # Get movie indices
            movie_indices = [i[0] for i in sim_scores]
            
            # Convert to movie records
            df = self.data_handler.df
            similar_movies = df.iloc[movie_indices].to_dict('records')
            
            return similar_movies
        except Exception as e:
            print(f"Error in get_similar_movies_improved: {e}")
            return []
    
    def get_personalized_recommendations(self, user_preferences, limit=10):
        """
        Get personalized recommendations based on user preferences
        
        Parameters:
        - user_preferences: dict with keys 'favorite_genres', 'favorite_directors', etc.
        - limit: Maximum number of recommendations to return
        
        Returns:
        - List of recommended movies
        """
        if not user_preferences:
            return self.get_popular_recommendations(limit)
        
        # Start with all movies
        df = self.data_handler.df.copy()
        
        # Skip if dataframe is empty
        if len(df) == 0:
            return []
        
        # Calculate a score for each movie based on user preferences
        favorite_genres = user_preferences.get('favorite_genres', [])
        favorite_directors = user_preferences.get('favorite_directors', [])
        favorite_actors = user_preferences.get('favorite_actors', [])
        
        # Initialize score column
        df['score'] = 0
        
        # Score based on genres
        if favorite_genres and 'genres_list' in df.columns:
            df['genre_score'] = df['genres_list'].apply(
                lambda x: sum(1 for genre in favorite_genres if genre in x)
            )
            df['score'] += df['genre_score'] * 2  # Weight genres more
        
        # Score based on directors
        if favorite_directors and 'director' in df.columns:
            df['director_score'] = df['director'].apply(
                lambda x: 3 if any(director.lower() in x.lower() for director in favorite_directors) else 0
            )
            df['score'] += df['director_score']
        
        # Score based on actors
        if favorite_actors and 'cast_list' in df.columns:
            df['actor_score'] = df['cast_list'].apply(
                lambda x: sum(1 for actor in favorite_actors if any(actor.lower() in cast.lower() for cast in x))
            )
            df['score'] += df['actor_score'] * 1.5
        
        # Add a small weight for highly rated movies
        if 'vote_average' in df.columns and 'vote_count' in df.columns:
            # Normalized rating score (0-1)
            vote_avg_max = df['vote_average'].max()
            vote_avg_min = df['vote_average'].min()
            if vote_avg_max > vote_avg_min:
                df['rating_norm'] = (df['vote_average'] - vote_avg_min) / (vote_avg_max - vote_avg_min)
                # Only consider movies with a minimum number of votes
                min_votes = 50  # Arbitrary threshold
                df.loc[df['vote_count'] < min_votes, 'rating_norm'] = 0
                df['score'] += df['rating_norm']
        
        # Get top scoring movies
        recommended = df.nlargest(limit, 'score')
        
        # If we don't have enough recommendations with non-zero scores,
        # fill with popular movies
        if len(recommended[recommended['score'] > 0]) < limit:
            zero_score_count = len(recommended[recommended['score'] == 0])
            if zero_score_count > 0:
                popular_movies = self.get_popular_recommendations(zero_score_count)
                # Replace zero-score movies with popular ones
                recommended = recommended[recommended['score'] > 0]
                popular_df = pd.DataFrame(popular_movies)
                if len(popular_df) > 0:
                    # Ensure we don't already have these movies in recommendations
                    existing_ids = set(recommended['id'])
                    popular_df = popular_df[~popular_df['id'].isin(existing_ids)]
                    recommended = pd.concat([recommended, popular_df.head(limit - len(recommended))])
        
        # Clean up temporary columns
        for col in ['score', 'genre_score', 'director_score', 'actor_score', 'rating_norm']:
            if col in df.columns:
                df = df.drop(col, axis=1)
        
        return recommended.to_dict('records')
    
    def get_recommendations_for_watchlist(self, watchlist, limit=10):
        """Get recommendations based on movies in user's watchlist"""
        if not watchlist:
            return self.get_popular_recommendations(limit)
        
        # Try using the hybrid approach first
        hybrid_recommendations = self.get_hybrid_recommendations(watchlist, limit)
        if hybrid_recommendations:
            return hybrid_recommendations
            
        # Fallback to the original method
        # Get similar movies for each movie in the watchlist
        all_similar = []
        for movie in watchlist:
            movie_id = movie.get('id')
            similar = self.get_similar_movies(movie_id, limit=5)  # Get 5 similar movies per watchlist item
            all_similar.extend(similar)
        
        # If we have no similar movies, return popular recommendations
        if not all_similar:
            return self.get_popular_recommendations(limit)
        
        # Count frequency of each movie in the recommendations
        movie_counts = {}
        for movie in all_similar:
            movie_id = movie.get('id')
            if movie_id not in movie_counts:
                movie_counts[movie_id] = {'count': 0, 'movie': movie}
            movie_counts[movie_id]['count'] += 1
        
        # Sort by frequency and get top movies
        sorted_movies = sorted(movie_counts.values(), key=lambda x: x['count'], reverse=True)
        top_movies = [item['movie'] for item in sorted_movies[:limit]]
        
        # If we don't have enough movies, pad with popular recommendations
        if len(top_movies) < limit:
            popular = self.get_popular_recommendations(limit - len(top_movies))
            # Add only movies not already in top_movies
            existing_ids = {movie.get('id') for movie in top_movies}
            for movie in popular:
                if movie.get('id') not in existing_ids and len(top_movies) < limit:
                    top_movies.append(movie)
        
        return top_movies
        
    def get_hybrid_recommendations(self, watchlist, limit=10):
        """
        Hybrid recommendation system that combines content-based and collaborative filtering
        
        Parameters:
        - watchlist: List of movies in the user's watchlist
        - limit: Maximum number of recommendations to return
        
        Returns:
        - List of recommended movies
        """
        try:
            if not watchlist or self.similarity_matrix is None:
                return []
                
            # Extract features from the watchlist movies
            watchlist_ids = [int(movie.get('id')) for movie in watchlist if movie.get('id')]
            
            # Filter valid movie IDs that exist in our indices
            valid_ids = [movie_id for movie_id in watchlist_ids if movie_id in self.movie_indices]
            
            if not valid_ids:
                return []
                
            # Get the indices of watchlist movies
            watchlist_indices = [self.movie_indices[movie_id] for movie_id in valid_ids]
            
            # Get user profile vector (average of watched movies' feature vectors)
            if len(watchlist_indices) > 0:
                user_profile = np.mean(self.feature_matrix[watchlist_indices, :], axis=0)
                
                # Calculate similarity between user profile and all movies
                user_similarity = cosine_similarity(user_profile.reshape(1, -1), self.feature_matrix).flatten()
                
                # Create a list of (index, similarity score) pairs
                sim_scores = list(enumerate(user_similarity))
                
                # Sort by similarity score
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                
                # Filter out movies already in watchlist
                sim_scores = [x for x in sim_scores if x[0] not in watchlist_indices][:limit+10]  # Get extra for diversity
                
                # Get movie indices
                movie_indices = [i[0] for i in sim_scores]
                
                # Add genre diversity (ensure we don't recommend too many of the same genre)
                df = self.data_handler.df
                selected_movies = []
                seen_genres = set()
                
                # Add movies with a focus on genre diversity
                for idx in movie_indices:
                    movie = df.iloc[idx]
                    
                    # Extract genres
                    if 'genres_list' in df.columns and isinstance(movie.get('genres_list'), list):
                        movie_genres = set(movie['genres_list'])
                        # If this movie adds at least one new genre, prioritize it
                        if movie_genres - seen_genres:
                            selected_movies.append(idx)
                            seen_genres.update(movie_genres)
                            if len(selected_movies) >= limit:
                                break
                
                # If we still need more movies, add the highest rated ones without genre consideration
                if len(selected_movies) < limit:
                    remaining = [idx for idx in movie_indices if idx not in selected_movies]
                    selected_movies.extend(remaining[:limit - len(selected_movies)])
                
                # Convert to movie records
                hybrid_recommendations = df.iloc[selected_movies[:limit]].to_dict('records')
                
                return hybrid_recommendations
                
            return []
        except Exception as e:
            print(f"Error in get_hybrid_recommendations: {e}")
            return []
