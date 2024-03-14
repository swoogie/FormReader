<script setup
        lang="ts">
        defineProps<{
            beingScanned: boolean;
        }>();
</script>

<template>
    <div class="grid grid-cols-3 opacity-95 columns-sm items-end mt-8">
        <div class="rounded h-fit w-20 px-3 m-4">
            <p class="text-md">Image Preview</p>
        </div>
        <button :disabled="beingScanned"
                class="object-left flex flex-col w-24 cursor-pointer items-center bg-green-600 transition-colors hover:bg-green-900 text-white m-auto p-2 rounded"
                :class="{ 'bg-green-900 cursor-default': beingScanned }"
                @click="$emit('scanform')">
            {{ beingScanned ? 'Scanning' : 'Scan' }}
            <i v-if="!beingScanned"
               class="bi bi-arrow-down animate-bounce"></i>
            <i v-if="beingScanned"
               class="bi bi-hourglass-split"></i>
        </button>
    </div>
</template>
