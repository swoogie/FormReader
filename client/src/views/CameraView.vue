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
        <p v-if="!isCaptureSupported()" class="text-center mb-4">
            Camera capture is not supported on this browser. Use a mobile browser instead. 
        </p>
        <i class="bi bi-camera-video-off text-9xl text-zinc-700"></i>
    </main>
</template>
