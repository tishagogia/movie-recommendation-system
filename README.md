# movie-recommendation-system
a Python-based Movie Recommendation System designed to help users discover and manage movies efficiently. The application provides a user-friendly interface with powerful tools for browsing, searching, and organizing films based on personal preferences.  

Key Features:  

1. User Registration & Login – A secure authentication system that protects user data while allowing personalized access to all features.  
2. Profile Management – Users can create detailed profiles, update their viewing preferences, maintain a complete watch history, and curate a list of favorite genres for tailored recommendations.  
3. Search & Filter Movies – An advanced search function that lets users quickly find movies by genre, director, actors, release year, and ratings, with options to sort results for maximum relevance.  
4. Bookmark Movies – A convenient watchlist feature that allows users to save interesting movies with one click and organize them into custom categories for future viewing.  
5. Movie Ratings & Reviews – An interactive rating system where users can share their opinions through star ratings and detailed reviews, helping others discover great films.  
6. Trending & Popular Movies – A dynamic section that highlights currently popular films based on real-time user activity and highest-rated movies according to community feedback.  
Architecture / Framework

•	Tkinter: Tkinter is used as the graphical user interface (GUI) framework for Movie Master. It provides a simple yet effective way to create interactive interfaces for users. Tkinter enables smooth navigation across different sections, such as movie search, watchlist, and trending movies. It ensures responsiveness and ease of use, making the application accessible to all users.
•	Pandas: Pandas is utilized for data processing, ensuring efficient handling of movie datasets. It enables quick filtering and retrieval of relevant movie recommendations based on user interactions.
•	NumPy & Scikit-Learn: These libraries power the recommendation system, analyzing user preferences and suggesting movies based on similarity algorithms and search history.
•	PIL (Pillow): PIL is used for image handling, allowing efficient management of movie posters and enhancing the visual experience.
•	CSV Dataset: Movie Master utilizes CSV files as the primary dataset for movie information. This dataset contains approximately 4,803 movies with details such as title, director, genre, release year, ratings, and cast. By leveraging structured CSV files, the application efficiently filters and retrieves movie recommendations based on user searches and preferences.
•	API Integration: An external API is used to fetch high-quality movie images and icons, enhancing the visual appeal of the application. This integration ensures that users can see official movie posters alongside their search results and recommendations.
•	The combination of Tkinter, Pandas, NumPy, Scikit-Learn, PIL, CSV datasets, and API integration ensures that Movie Master is robust, scalable, and user-friendly.
