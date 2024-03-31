import axios from "axios";

export async function postImage(image: File): Promise<{checkbox: number[][], inputField: number[][]}> {
    const formData = new FormData();
    formData.append('file', image);
    const response = (await axios.post('/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })).data;
    return {
        checkbox: response['checkbox_coordinates'],
        inputField: response['input_field_coordinates']
    }
}