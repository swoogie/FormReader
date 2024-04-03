import axios from "axios";

interface ImageApiResponse {
    checkbox: number[][],
    inputLine: number[][],
    charBox: number[][]
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
        inputLine: response['input_line_coords'],
        charBox: response['char_input_coords']
    }
}