<script setup lang="ts">
    defineProps<{
        disabled: boolean;
    }>();
</script>

<template>
    <label for="fileInput"
           class="flex justify-center cursor-pointer items-center dark:bg-zinc-800 transition-colors dark:hover:bg-zinc-900 bg-zinc-200 hover:bg-zinc-300 rounded">
        <i class="text-3xl bi bi-file-earmark-arrow-up"></i>
        <input :disabled="disabled"
               id="fileInput"
               type="file"
               class="hidden"
               accept="image/png, image/jpeg, image/jpg" />
    </label>
</template>