import axios from "axios";

export function postImage(image: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', image);
    return axios.post('http://127.0.0.1:5000/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(response => response.data);
}