<script setup
        lang="ts">
        function isCaptureSupported() {
            const input = document.createElement('input');
            input.type = 'file';

            return 'capture' in input;
        }
</script>

<template>
    <main class="flex flex-col place-content-center place-items-center">
        <i class="bi bi-camera-video-off text-9xl text-zinc-700/50"></i>
        <p v-if="!isCaptureSupported()" class="text-center mt-2">
            Camera capture is not supported on this browser. Use a mobile browser instead. 
        </p>
    </main>
</template>
