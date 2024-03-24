<script setup
        lang="ts">
        function isCaptureSupported() {
            const input = document.createElement('input');
            input.type = 'file';

            return 'capture' in input;
        }
</script>

<template>
    <main>
        <p v-if="!isCaptureSupported()" class="flex place-content-center place-items-center">
            Camera capture is not supported on this browser. Try a mobile browser instead. 
        </p>
    </main>
</template>
