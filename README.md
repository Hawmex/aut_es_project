# Expert Systems

This repository contains the files of my project for the "Expert Systems" course at AUT (Tehran Polytechnic).

## Project: Movie Recommendation

This project implements a movie recommendation system using an expert system approach. It leverages a rule-based inference engine to recommend movies from The Movie Database (TMDb) API based on user preferences such as mood, favorite genre, movie vibe, era, duration, and rating.

### Project Structure

- **`app.py`**: The main entry point of the application. It integrates the inference engine with the TMDb API to fetch and display movie recommendations based on the inferred query.
- **`rulebase.py`**: Defines the rulebase with a set of rules combining user inputs (e.g., mood, genre, vibe, era, duration, rating) to generate movie search queries.
- **`core/inference_engine.py`**: Implements the inference engine, which processes the rulebase and interactively collects user inputs to infer a movie query.
- **`core/rulebase/dependency.py`**: Defines the `Dependency` class for managing dependencies and priorities of input variables.
- **`core/rulebase/expression.py`**: Contains classes for expressions (`Assignment` and `Evaluation`) used in rule conditions and actions.
- **`core/rulebase/logical_operator.py`**: Implements logical operators (`LogicalAnd` and `LogicalOr`) for combining expressions in rules.
- **`core/rulebase/rule.py`**: Defines the `Rule` class, which combines antecedents (conditions) and consequents (actions) for the inference process.
- **`core/rulebase/rulebase.py`**: Defines the `Rulebase` class, which manages the collection of rules and their input/output dependencies.
- **`core/rulebase/types.py`**: Contains type definitions for the state and dependencies used across the system.
- **`core/rulebase/statement.py`**: Defines the abstract `Statement` class, which is the base for expressions and logical operators.

### How It Works

1. **User Interaction**:

   - The system prompts the user to answer questions about their preferences (e.g., mood, favorite genre, movie vibe, era, duration, rating).
   - Users can skip questions by pressing Enter, allowing flexibility in input.

2. **Inference Engine**:

   - The `InferenceEngine` class evaluates rules from `rulebase.py` based on user inputs.
   - It prioritizes rules by the importance of their dependencies and collects missing inputs interactively.
   - The engine infers a query by matching user inputs against rule conditions and applying the corresponding actions.

3. **Query Refinement**:

   - The inferred query is refined in `app.py` by mapping user-friendly terms (e.g., genre names, keywords) to TMDb API-compatible values (e.g., genre IDs, keyword IDs).
   - The system uses the TMDb API to fetch movie data based on the refined query.

4. **Output**:
   - The recommended movies are displayed in a formatted table, including title, release date, vote average, and vote count.

### Key Features

- **Rule-Based System**: 28 predefined rules in `rulebase.py` cover various combinations of user mood, genre, vibe, era, duration, and rating preferences.
- **Dynamic Query Generation**: The system dynamically constructs API queries based on user inputs and rule outcomes.
- **TMDb API Integration**: Fetches real-time movie data using the TMDb API, requiring an API token stored in a `.env` file.
- **Flexible Input Handling**: Users can skip questions, and the system adapts by evaluating only applicable rules.
- **Extensible Design**: The modular structure allows easy addition of new rules or modifications to existing ones.

### Setup and Installation

1. **Prerequisites**:

   - Python 3.8+
   - A TMDb API token (obtain from [TMDb](https://www.themoviedb.org/))

2. **Installation**:

   ```bash
   pip install requests pandas python-dotenv
   ```

3. **Configuration**:

   - Create a `.env` file in the project root with your TMDb API token:
     ```plaintext
     TMDB_TOKEN=your_api_token_here
     ```

4. **Running the Application**:
   ```bash
   python app.py
   ```

### Usage

- Run `app.py` to start the interactive prompt.
- Answer questions about your movie preferences (e.g., "What is your mood?" or "What is your favorite genre?").
- Press Enter to skip any question.
- The system will infer a query, display it, and fetch movie recommendations from TMDb.
- View the recommended movies in a table format.

### Example Rules

- **Happy + Comedy**: Recommends feel-good comedies with a minimum vote average of 6.5.
- **Sad + Cathartic**: Suggests high-quality emotional dramas sorted by vote average.
- **Adventurous + Epic Journey**: Finds quest-based adventure or fantasy films with a minimum vote average of 7.0.
- **Modern Classic + Drama/Crime**: Recommends highly rated drama or crime films from 2000–2015.

### Limitations

- Requires a valid TMDb API token.
- Limited to the predefined rules in `rulebase.py`.
- Internet connection required for API calls.
- Skipped questions may result in fewer or no recommendations if insufficient information is provided.

### Future Improvements

- Add support for more complex rule combinations or user-defined rules.
- Implement caching for API responses to reduce redundant calls.
- Enhance the user interface (e.g., GUI or web-based frontend).
- Expand rulebase to include more genres, vibes, or other criteria like specific actors or directors.

### Acknowledgments

- The Movie Database (TMDb) for providing the movie data API.
- AUT (Tehran Polytechnic) for the "Expert Systems" course inspiration.
