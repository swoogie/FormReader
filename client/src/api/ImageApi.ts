import axios from "axios";

export async function postImage(image: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', image);
    return (await axios.post('/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })).data['checkbox_coordinates'];
}