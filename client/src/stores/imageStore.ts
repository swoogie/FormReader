import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useImageStore = defineStore('imageStore', () => {
  const uploadedImage = ref();
  const processedImage = ref();
  function addImage(image: any) {
    uploadedImage.value = image;
  }
  function removeImage() {
    uploadedImage.value = null;
  }
  function addProcessedImage(image: any) {
    uploadedImage.value = image;
  }
  function removeProcessedImage() {
    uploadedImage.value = null;
  }

  return { uploadedImage, processedImage, addImage, removeImage, addProcessedImage, removeProcessedImage }
})
