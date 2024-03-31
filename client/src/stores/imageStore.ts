import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useImageStore = defineStore('imageStore', () => {
    const uploadedImage = ref();
    const processedImage = ref();

    const loadState = () => {
        uploadedImage.value = JSON.parse(localStorage.getItem("processedImage") || '""');
        processedImage.value = JSON.parse(localStorage.getItem("processedImage") || '""');
    };
    loadState();

    function addImage(image: any) {
        uploadedImage.value = image;
        localStorage.setItem('uploadedImage', JSON.stringify(image));
    }
    function removeImage() {
        uploadedImage.value = null;
        localStorage.removeItem('uploadedImage');
    }
    function addProcessedImage(image: any) {
        uploadedImage.value = image;
        localStorage.setItem('processedImage', JSON.stringify(image));
    }

    function removeProcessedImage() {
        uploadedImage.value = null;
        localStorage.removeItem('processedImage');
    }

    return { uploadedImage, processedImage, addImage, removeImage, addProcessedImage, removeProcessedImage }
})
