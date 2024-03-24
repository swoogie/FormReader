<script setup
        lang="ts">
        import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
        import { ref, watch } from 'vue';
        import HelloWorld from './components/HelloWorld.vue'

        const pageTitle = ref("Form Reader");
        const msg = ref("Welcome! Login to see your forms");

        function getPathTitle(path: string) {
            let title: string = path.substring(1);
            title = title.charAt(0).toUpperCase() + title.substring(1);
            return title;
        }
        const route = useRoute();
        const allRoutes = useRouter().getRoutes().map((route) => route.path);
        watch(() => route.path, (newPath) => {
            if (!allRoutes.includes(newPath)) {
                pageTitle.value = "404";
                msg.value = "Page not found";
                return;
            }
            switch (newPath) {
                case '/': pageTitle.value = "Form Reader"; break;
                default: pageTitle.value = getPathTitle(newPath); break;
            }
            switch (newPath) {
                case '/': msg.value = "Welcome!"; break;
                case '/camera': msg.value = "Take a picture of your form"; break;
                case '/upload': msg.value = "Upload your form"; break;
                default: msg.value = " "; break;
            }
        })
</script>

<template>
    <header class="flex justify-center mx-auto max-w-md leading-6 border-b border-gray-500 p-2">
        <div>
            <HelloWorld :pageTitle="pageTitle"
                        :msg="msg" />
            <nav class="w-full font-medium text-center mt-7">
                <RouterLink class="px-2 duration-150 transition-colors hover:bg-green-400 hover:bg-opacity-50"
                            to="/">Home</RouterLink>
                <RouterLink class="px-2 duration-150 border-l border-gray-500 transition-colors hover:bg-green-400 hover:bg-opacity-50"
                            to="/camera">Camera</RouterLink>
                <RouterLink class="px-2 duration-150 border-l border-gray-500 transition-colors hover:bg-green-400 hover:bg-opacity-50"
                            to="/upload">Upload</RouterLink>
            </nav>
        </div>
    </header>

    <RouterView />
</template>

<style scoped>
nav a.router-link-exact-active {
    @apply text-green-400 bg-transparent;
}
</style>