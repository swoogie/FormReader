import axios from "axios";

export async function postImage(image: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', image);
    return (await axios.post('http://127.0.0.1:8080/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })).data['checkbox_coordinates'];
}