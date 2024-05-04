<script setup
        lang="ts">
        import { ref } from "vue";
        const isDraggedOver = ref<boolean>(false);
</script>
<template>
    <label for="fileInput"
           @dragover.prevent="isDraggedOver = true;"
           @dragleave.prevent="isDraggedOver = false;"
           class="group flex flex-col items-center justify-center px-10 
           w-[70svw] max-w-[700px] max-h-[500px] h-[50svh] 
           border-dashed border-gray-500 border-2 rounded-md cursor-pointer"
           :class="{ 'border-green-500': isDraggedOver }">
        <input id="fileInput"
               type="file"
               class="hidden"
               accept="image/png, image/jpeg, image/jpg" />
        <i class="bi bi-file-earmark-arrow-up text-9xl text-zinc-700/50
           animate-pulse group-hover:animate-none group-hover:primary-gradient-text"></i>
        <p class="mt-7 transition-all text-xs sm:text-base">Drag and drop your .png or .jp(e)g image here or click to
            select.</p>
    </label>
</template>
