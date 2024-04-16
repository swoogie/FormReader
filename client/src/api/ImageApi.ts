import axios from "axios";

interface ImageApiResponse {
    checkbox: number[][],
    inputLine: number[][],
    charBox: number[][],
    resolution: number[]
}

export async function postImage(image: File): Promise<ImageApiResponse> {
    const formData = new FormData();
    formData.append('file', image);
    const response = (await axios.post('/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })).data;
    return {
        checkbox: response['checkbox_coords'],
        inputLine: response['line_coords'],
        charBox: response['char_input_coords'],
        resolution: response['resolution']
    }
}

// export async function postImageForCropping(image: File): Promise<any> {
//     const formData = new FormData();
//     formData.append('file', image);
//     axios.post('http://127.0.0.1:5000/image', { responseType: 'blob' })
//         .then(response => {
//             const imageUrl = URL.createObjectURL(response.data); // response.data is the imageBlob
//             const imageElement = document.getElementById('myImage') as HTMLImageElement;
//             imageElement.src = imageUrl;
//             return 
//         })
//         .catch(error => console.error('Error fetching image:', error));
// }

export async function postImageForCropping(image: File) {
    const formData = new FormData();
    formData.append('file', image);
    try {
        const response = await axios.post('/crop', formData, { responseType: 'blob' });
        return URL.createObjectURL(response.data);
    } catch (error) {
        console.error('Error fetching image:', error);
    }
}