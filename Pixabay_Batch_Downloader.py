import requests
import os

def download_pixabay_images(api_key, query, total_images, base_save_dir):
    per_page = 200  

    num_pages = (total_images + per_page - 1) // per_page

    query_save_dir = os.path.join(base_save_dir, query)

    if not os.path.exists(query_save_dir):
        os.makedirs(query_save_dir)

    count = 0  

    for page in range(1, num_pages + 1):
        url = f"https://pixabay.com/api/?key={api_key}&q={query}&per_page={per_page}&page={page}"

        try:
            response = requests.get(url)
            data = response.json()

            if "hits" in data:
                hits = data["hits"]

                for hit in hits:
                    if count >= total_images:
                        break  

                    image_url = hit["largeImageURL"]
                    response = requests.get(image_url)

                    if response.status_code == 200:
                        file_extension = image_url.split(".")[-1]
                        file_name = f"{hit['id']}.{file_extension}"
                        file_path = os.path.join(query_save_dir, file_name)

                        with open(file_path, "wb") as file:
                            file.write(response.content)
                        
                        count += 1  
                    else:
                        print(f"Failed to download image: {image_url}")

            else:
                print("Failed to retrieve data from Pixabay")

        except Exception as e:
            print(f"There is an error: {str(e)}")

if __name__ == "__main__":
    api_key = "1234567890"  # Replace it with your Pixabay API key
    query = "night+sky"  # Replace it with your search keyword, use + to replace the space in the keyword
    total_images = 10  # The total number of images you want to download
    base_save_directory = r"C:\Users\Afkar\Pictures"  # Storage base directory, change "Afkar" with your username

    download_pixabay_images(api_key, query, total_images, base_save_directory)
