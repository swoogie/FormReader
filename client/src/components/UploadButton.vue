<template>
    <label for="fileInput"
           class="flex justify-center cursor-pointer items-center bg-zinc-800 transition-colors hover:bg-zinc-900 text-white size-32 rounded">
        <i class="text-3xl bi bi-file-earmark-arrow-up"></i>
        <input id="fileInput"
               type="file"
               class="hidden"
               accept="image/png, image/jpeg, image/jpg" />
    </label>
</template>