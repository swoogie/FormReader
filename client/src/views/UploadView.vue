<script setup
        lang="ts">
        import UploadLoader from "@/components/UploadLoader.vue";
        import PreviewHeader from "@/components/PreviewHeader.vue";
        import ModalComponent from "@/components/ModalComponent.vue";
        import DragAndDrop from "@/components/DragAndDrop.vue";
        import { useImageStore } from "@/stores/imageStore";
        import { postImage } from "@/api/ImageApi";
        import { ref, nextTick } from "vue";


        let file: File;
        let resolution: {width: number, height: number};
        const imageStore = useImageStore();
        const fileName = ref<string>('');
        const beingScanned = ref<boolean>(false);
        const showModal = ref<boolean>(false);
        const error = ref<string>('');
        const checkboxCoords = ref<number[][]>();
        const scannedImage = ref<HTMLImageElement>();
        const domToActualRatio = ref<number>();

        async function handleUpload($event: Event) {
            if ($event instanceof DragEvent && $event.dataTransfer?.files[0]) {
                file = $event.dataTransfer?.files[0] as File;
                console.log(file);
            } else {
                const inputTarget = $event.target as HTMLInputElement;
                if (!inputTarget.files?.[0]) return;
                file = inputTarget.files[0];
            }
            const fileReader = new FileReader();
            fileReader.onload = async (e) => {
                const imageDataUrl = e.target?.result as string;
                imageStore.addImage(imageDataUrl);
                resolution = await new Promise((resolve) => {
                    const image = new Image();
                    image.src = imageDataUrl;
                    image.onload = () => {
                        resolve({width: image.naturalWidth, height: image.naturalHeight});
                    };
                });
            };
            await new Promise<void>((resolve) => {
                fileReader.onloadend = () => resolve();
                fileReader.readAsDataURL(file);
            });
            fileName.value = file['name'];
        }

        async function scanForm() {
            showModal.value = false;
            beingScanned.value = true;
            try {
                checkboxCoords.value = await postImage(file);
                beingScanned.value = false;
                error.value = '';
            } catch (e: any) {
                error.value = e.message;
                beingScanned.value = false;
                return;
            }
            showModal.value = true;
            await nextTick();
            if (scannedImage.value) {
                const { width } = scannedImage.value.getBoundingClientRect();
                domToActualRatio.value = width / resolution.width;
                checkboxCoords.value = checkboxCoords.value?.map((coords) => {
                    return coords.map((coords) => coords * (domToActualRatio.value ?? 0));
                })
            } 
            beingScanned.value = false;
        }

</script>

<template>
    <main class="flex flex-col items-center transition-all relative h-5/6">
        <DragAndDrop @drop.stop.prevent="handleUpload"
                     @change="handleUpload" />
        <PreviewHeader v-if="imageStore.uploadedImage"
                       :being-scanned="beingScanned"
                       @scanform="scanForm"
                       @click="handleUpload" />

        <div class="relative">
            <div v-if="beingScanned"
                 class="absolute flex items-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                <UploadLoader />
            </div>
            <div v-if="error && !beingScanned"
                 class="absolute flex flex-col justify-center items-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                <i class="bi bi-exclamation-triangle text-3xl"></i>
                <p>Error: {{ error }}</p>
            </div>
            <img v-if="imageStore.uploadedImage"
                 class="max-h-[32rem] rounded-lg object-contain"
                 :src="imageStore.uploadedImage" />
        </div>
        <p v-if="fileName"
           class="ms-2">{{ fileName }}</p>

        <ModalComponent @close="showModal = false;"
                        :isVisible="showModal">
            <template #header>
                {{ fileName }}
            </template>
            <div class="relative">
                <input v-for="(coords, index) in checkboxCoords"
                       :key="index"
                       type="checkbox"
                       class="absolute"
                       :style="`top: ${coords[1]}px; left: ${coords[0]}px`">
                <img v-if="imageStore.uploadedImage"
                     class="max-h-[36rem] object-contain rounded-sm"
                     :src="imageStore.uploadedImage"
                     ref="scannedImage" />
            </div>
            <template #footer>
                <button class="transition-colors bg-green-600 hover:bg-green-900 rounded-md mx-auto mt-2 size-10">
                    <i class="bi bi-download text-2xl"></i>
                </button>
            </template>
        </ModalComponent>
    </main>
</template>
