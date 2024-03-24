<script setup
        lang="ts">
        import UploadButton from "@/components/UploadButton.vue";
        import { useImageStore } from "@/stores/imageStore";
        import { ref } from "vue";
        const imageStore = useImageStore();
        const isDraggedOver = ref<boolean>(false);
</script>
<template>
    <label v-if="!imageStore.uploadedImage"
           for="fileInput"
           @dragover.prevent="isDraggedOver = true;"
           @dragleave.prevent="isDraggedOver = false;"
           class="flex flex-col items-center justify-center px-10 w-[70svw] max-w-[700px] max-h-[500px] h-[50svh] border-dashed border-gray-500 border-2 rounded-md"
           :class="{ 'border-green-500': isDraggedOver }">
        <UploadButton />
        <p class="mt-7">Drag and drop your .png or .jp(e)g image here or click to select.</p>
    </label>
</template>
