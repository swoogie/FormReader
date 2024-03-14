<script setup
        lang="ts">
        import UploadButton from "@/components/UploadButton.vue";
        import UploadLoader from "@/components/UploadLoader.vue";
        import ScanButton from "@/components/ScanButton.vue";
        import { postImage } from "@/api/ImageApi";
        import { ref } from "vue";

        let file: File | null = null;
        const fileName = ref<string>('');
        const imagePreview = ref<string>('');
        const beingScanned = ref<boolean>(false);

        async function handleUpload($event: Event) {
            const inputTarget = $event.target as HTMLInputElement;
            if (inputTarget.files === null) return;
            file = inputTarget.files[0];
            console.log(inputTarget.files[0]);
            const fileReader = new FileReader();
            fileReader.onload = (e) => {
                imagePreview.value = e.target?.result as string;
            };
            await new Promise((resolve) => {
                fileReader.onloadend = resolve;
                if (file === null) return;
                fileReader.readAsDataURL(file);
            });
            fileName.value = file['name'];
        }

        async function scanForm() {
            beingScanned.value = true;
            if (file) postImage(file);
            await new Promise((resolve) => setTimeout(resolve, 5000));
            beingScanned.value = false;
        }

        const isDraggedOver = ref<boolean>(false);
        function dragover($event: DragEvent) {
            isDraggedOver.value = true;
            console.log($event);
        }
        
        function dragleave($event: DragEvent) {
            isDraggedOver.value = false;
            console.log($event);
        }

</script>

<template>
    <main class="flex flex-col items-center">
        <div class="transition-all relative h-5/6">
            <label for="fileInput" 
                 @dragover="dragover"
                 @dragleave="dragleave"
                 class="transition-color duration-150 flex flex-col items-center justify-center mt-8 px-10 max-w-[700px] w-[80svw] max-h-[500px] h-[60svh] border-dashed border-gray-500 border-2 rounded-md"
                 :class="{'border-green-500': isDraggedOver}"
                 >
                <UploadButton @change="handleUpload" />
                <p class="mt-7">Drag and drop your .png or .jpeg image here or click to select.</p>
            </label>
            <ScanButton v-if="imagePreview"
                        :being-scanned="beingScanned"
                        @scanform="scanForm" />
            <div class="relative">
                <div v-if="beingScanned"
                     class="absolute flex items-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                    <UploadLoader />
                </div>
                <img v-if="imagePreview"
                     class="max-h-[36rem] rounded-lg object-contain"
                     :src="imagePreview"
                     alt="image" />
            </div>
            <p v-if="fileName"
               class="ms-2">{{ fileName }}</p>
        </div>
    </main>
</template>
