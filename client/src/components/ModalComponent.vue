<script setup
        lang="ts">
        import { defineProps, ref, watch } from 'vue';

        const props = defineProps<{
            isVisible: boolean
        }>();

        const isVisible = ref<boolean>(props.isVisible);

        const emit = defineEmits(['close']);

        const closeModal = () => {
            emit('close');
            isVisible.value = false;
        };
        watch(() => props.isVisible, (newVal) => {
            isVisible.value = newVal;
        });
</script>

<template>
    <div v-if="isVisible"
         class="backdrop-blur-sm fixed inset-0 z-50 overflow-y-auto flex justify-center items-center">
        <div @click.self="closeModal"
             class="fixed inset-0 bg-gray-700 bg-opacity-50"></div>
        <div class="flex flex-col backdrop-blur-sm bg-white/70 dark:bg-zinc-800/70 p-2 rounded-md shadow-md">
            <div class="pb-2 relative">
                <button @click="closeModal"
                        class="absolute px-1">
                    <i class="bi bi-x-lg"></i>
                </button>
                <div class="text-center">
                    <slot name="header"></slot>
                </div>
            </div>
            <div class="flex-grow">
                <slot></slot>
            </div>
            <slot name="footer"></slot>
            <div class="mt-auto">
            </div>
        </div>
    </div>
</template>