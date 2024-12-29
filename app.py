import os
import argparse
from openai import OpenAI


def get_api_key(args):
    """
    Get API key from command line argument or environment variable.
    Priority: Command line argument > Environment variable
    
    Args:
        args: Parsed command line arguments
    
    Returns:
        str: API key if found, None otherwise
    """
    if args.api_key:
        return args.api_key
    return os.getenv('OPENAI_API_KEY')


def generate_story(genre, api_key):
    """
    Generate a story based on the given genre using OpenAI's GPT model.
    
    Args:
        genre (str): The genre of the story (e.g., fantasy, mystery, romance)
        api_key (str): OpenAI API key
    
    Returns:
        str: Generated story
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Create a prompt based on the genre
    prompt = f"""Write a short story in the {genre} genre. 
    The story should be approximately 200 words long and have a clear 
    beginning, middle, and end."""
    
    # Generate the story using GPT
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a creative story writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating story: {str(e)}"


def main():
    """
    Main function to run the story generator application.
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate stories ' +
                                     'using OpenAI GPT')
    parser.add_argument('--api-key', help='OpenAI API key')
    args = parser.parse_args()
    
    # Get API key
    api_key = get_api_key(args)
    if not api_key:
        print("Error: No API key provided. Please provide it either" + 
              "as a command line argument or set OPENAI_API_KEY environment" +
              " variable.")
        return
    
    print("Welcome to the Simple Story Generator!")
    print("\nAvailable genres:")
    print("1. Fantasy")
    print("2. Mystery")
    print("3. Romance")
    print("4. Science Fiction")
    print("5. Horror")
    
    # Get user input
    genre_choice = input("\nEnter the number of your chosen genre (1-5): ")
    
    # Map number to genre
    genres = {
        "1": "fantasy",
        "2": "mystery",
        "3": "romance",
        "4": "science fiction",
        "5": "horror"
    }
    
    if genre_choice in genres:
        print(f"\nGenerating a {genres[genre_choice]} story...")
        story = generate_story(genres[genre_choice], api_key)
        print("\nYour generated story:\n")
        print(story)
    else:
        print("Invalid genre choice. Please select a number between 1-5.")


if __name__ == "__main__":
    main()