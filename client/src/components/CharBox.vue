<script setup
        lang="ts">
        function nextSibling(event: Event) {
            const nextElement = (event.target as HTMLElement).nextElementSibling as HTMLInputElement;
            if (nextElement) {
                nextElement.focus();
            }
        }

        function checkWhichKeyDown(event: KeyboardEvent) {
            if (event.code === 'ArrowRight') {
                ((event.target as HTMLElement)?.nextElementSibling as HTMLElement).focus();
            }
            if (event.code === 'ArrowLeft') {
                ((event.target as HTMLElement)?.previousElementSibling as HTMLElement).focus();
            }
            if (event.code === 'Backspace') {
                ((event.target as HTMLElement)?.previousElementSibling as HTMLElement).focus();
            }
        }
</script>
<template>
    <input type="text"
           maxlength="1"
           class="absolute bg-transparent text-black text-base"
           @input="nextSibling"
           @keydown="checkWhichKeyDown"
           style="font-family: Arial">
</template>
