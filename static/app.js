document.getElementById("submit-btn").addEventListener("click", async function () {
  const genre = document.getElementById("genre").value;
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = ""; // Clear previous results

  try {
    console.log("Sending genre:", genre); // Log genre before sending
    const response = await axios.post("/suggest_movies", { genre }, {
      headers: { 'Content-Type': 'application/json' }
    });
    const movies = response.data.movies;

    if (movies.length > 0) {
      const ul = document.createElement("ul");
      movies.forEach(movie => {
        const li = document.createElement("li");
        li.textContent = `${movie.name} (Rating: ${movie.rating})`;
        ul.appendChild(li);
      });
      resultsDiv.appendChild(ul);
    } else {
      resultsDiv.textContent = "No movies found for this genre.";
    }
  } catch (error) {
    console.error("Error fetching movie suggestions:", error);
    resultsDiv.textContent = "An error occurred while fetching movie suggestions.";
  }
});
