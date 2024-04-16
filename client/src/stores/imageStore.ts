import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useImageStore = defineStore('imageStore', () => {
    const uploadedImage = ref();
    const processedImage = ref();
    const storedFile = ref();

    function addImage(imageDataUrl: any, file: any) {
        uploadedImage.value = imageDataUrl;
        storedFile.value = file;
    }

    function removeImage() {
        uploadedImage.value = null;
        storedFile.value = null;
    }

    function addProcessedImage(imageDataUrl: any) {
        processedImage.value = imageDataUrl;
    }

    function removeProcessedImage() {
        processedImage.value = null;
    }

    return { storedFile, uploadedImage, processedImage, addImage, removeImage, addProcessedImage, removeProcessedImage }
})
