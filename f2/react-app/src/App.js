import './App.css';
import { useState, useEffect } from 'react';
import SearchIcon from './search.svg';
import MovieCard from './MovieCard';

// APIkey: e8914733

const API_URL = "http://www.omdbapi.com?apikey=e8914733"

const App = () => {
  const [ movies, setMovies ] = useState([]);
  const [searchTerm, setSearchTerm ] = useState('')

  const searchMovies = async (title) => {
    const response = await fetch(`${API_URL}&s=${title}`);
    const data = await response.json();

    setMovies(data.Search);
    }
  
  useEffect(() => {
    searchMovies('Lost in Translation');
  }, []); // with the array [], means data is only called at upon each new GET; may want to change this for our app
  
  return (
    <div className="app">
      <h1>MovieLand</h1>
      <div className="search">
        <input
        placeholder="Search for movies" 
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        />
        <img
          src={SearchIcon}
          alt="search"
          onClick={() => searchMovies(searchTerm)}
          />
      </div>
      
      {
        movies?.length > 0
          ? (
            <div className="container">
              {movies.map((movie) => (
                <MovieCard movie={movie}/>
              ))}
          </div>
        ) : (
          <div class="empty">
            <h2>No Movies Found</h2>
          </div>
        )}

      <div className="footer">
        <footer>Copyright 2023 &copy; All Rights Reserved</footer>
      </div>
    </div>
  );
}

export default App;
