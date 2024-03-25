<script setup
        lang="ts">
        import { onMounted, ref } from "vue";
        const start1 = ref<boolean>(false);
        const start2 = ref<boolean>(false);
        const start3 = ref<boolean>(false);

        const delay = () => new Promise((resolve) => setTimeout(resolve, 100)); 

        onMounted(async () => {
            start1.value = true;
            await delay();
            start2.value = true;
            await delay();
            start3.value = true;
        })
</script>

<template>
    <div class="flex text-2xl justify-center w-full">
        <i class="bi bi-dot w-5"
           :class="{ 'animate-bounce': start1 }"></i>
        <i class="bi bi-dot w-5"
           :class="{ 'animate-bounce': start2 }"></i>
        <i class="bi bi-dot w-5"
           :class="{ 'animate-bounce': start3 }"></i>
    </div>
</template>