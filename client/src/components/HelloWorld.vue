<script setup
        lang="ts">
        defineProps<{
            pageTitle: string,
            msg: string
        }>()
</script>

<template>
    <div class="text-center">
        <h1 class="font-medium text-3xl sm:text-4xl relative -top-3 primary-gradient-text">
            {{ pageTitle }}</h1>
        <h3 class="font-light">{{ msg }}</h3>
    </div>
</template>
