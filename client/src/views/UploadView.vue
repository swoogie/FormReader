<script setup
        lang="ts">
        import UploadLoader from "@/components/UploadLoader.vue";
        import PreviewHeader from "@/components/PreviewHeader.vue";
        import ModalComponent from "@/components/ModalComponent.vue";
        import DragAndDrop from "@/components/DragAndDrop.vue";
        import CustomCheckbox from "@/components/CustomCheckbox.vue";
        import CharBox from "@/components/CharBox.vue";
        import InputField from "@/components/InputField.vue";
        import { useImageStore } from "@/stores/imageStore";
        import { postImage, postImageForCropping } from "@/api/ImageApi";
        import { ref } from "vue";
        import { jsPDF } from "jspdf";


        let resolution: number[];
        const imageStore = useImageStore();
        const fileName = ref<string>('');
        const beingScanned = ref<boolean>(false);
        const showModal = ref<boolean>(false);
        const error = ref<string>('');
        const checkboxCoords = ref<number[][]>();
        const inputFieldCoords = ref<number[][]>();
        const charBoxCoords = ref<number[][]>();
        const domToActualRatio = ref<number>();
        const form = ref<HTMLElement>();

        async function handleUpload($event: Event) {
            let file: File;
            if ($event instanceof DragEvent && $event.dataTransfer?.files[0]) {
                file = $event.dataTransfer?.files[0] as File;
            } else {
                const inputTarget = $event.target as HTMLInputElement;
                if (!inputTarget.files?.[0]) return;
                file = inputTarget.files[0];
            }
            const fileReader = new FileReader();
            fileReader.onload = async (e) => {
                const imageDataUrl = e.target?.result as string;
                imageStore.addImage(imageDataUrl, file);
            };
            await new Promise<void>((resolve) => {
                error.value = '';
                fileName.value = file['name'];
                fileReader.readAsDataURL(file);
                fileReader.onloadend = () => resolve();
            });
        }

        function mapToRatio(elementCoords: number[][], offset: number = 0) {
            return elementCoords.map((coords) => {
                return coords.map((coords) => (coords * (domToActualRatio.value ?? 0) - offset));
            });
        }

        async function scanForm() {
            showModal.value = false;
            beingScanned.value = true;
            await Promise.all([postImage(imageStore.storedFile), postImageForCropping(imageStore.storedFile)]).then((values) => {
                checkboxCoords.value = values[0].checkbox;
                inputFieldCoords.value = values[0].inputLine;
                charBoxCoords.value = values[0].charBox.reverse();
                resolution = values[0].resolution;
                imageStore.addProcessedImage(values[1]);
            }).catch((e) => {
                error.value = e.message;
                beingScanned.value = false;
            });
            beingScanned.value = false;
            showModal.value = true;
        }

        function download() {
            const doc = new jsPDF();
            if (!form.value) return;
            doc.html(form.value, {
                html2canvas: {
                    scale: domToActualRatio.value,
                    logging: true,
                    scrollX: 0,
                    scrollY: 0,
                    windowWidth: resolution[0],
                    windowHeight: resolution[1],
                },
                callback: function (doc) {
                    doc.save();
                }
            });
        }

        function removeImage() {
            imageStore.removeImage();
            fileName.value = '';
            error.value = '';
        }

        function imageLoaded(event: Event) {
            const img = event.target as HTMLImageElement;
            if (resolution) {
                domToActualRatio.value = img.width / resolution[0];
                checkboxCoords.value = mapToRatio(checkboxCoords.value ?? [], 2.5)
                inputFieldCoords.value = mapToRatio(inputFieldCoords.value ?? [], 2.5)
                charBoxCoords.value = mapToRatio(charBoxCoords.value ?? [], 2.5)
            }
        }
</script>

<template>
    <main class="flex flex-col items-center relative h-5/6">
        <DragAndDrop @drop.stop.prevent="handleUpload"
                     @change="handleUpload" />
        <PreviewHeader v-if="imageStore.uploadedImage"
                       :being-scanned="beingScanned"
                       @scanform="scanForm"
                       @change.stop="handleUpload" />

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
                 class="max-h-[50svh] rounded-lg object-contain"
                 :src="imageStore.uploadedImage" />
        </div>
        <p v-if="imageStore.uploadedImage"
           class="ms-2">{{ fileName }}
            <button @click="removeImage">
                <i class="text-red-500 bi bi-x-lg"></i>
            </button>
        </p>

        <ModalComponent @close="showModal = false;"
                        :isVisible="showModal">
            <template #header>
                {{ fileName }}
            </template>
            <div class="relative"
                 ref="form">
                <CustomCheckbox v-for="(coords, index) in checkboxCoords"
                                :key="index"
                                :style="`left: ${coords[0]}px; top: ${coords[1]}px;`" />
                <CharBox v-for="(coords, index) in charBoxCoords"
                         :key="index"
                         :style="`left: calc(${coords[0]}px + 3px); top: calc(${coords[1]}px + 2px); width: ${coords[2] - coords[0]}px; height: ${coords[3] - coords[1]}px`" />
                <InputField v-for="(coords, index) in inputFieldCoords"
                            :key="index"
                            :style="`left: ${coords[0]}px; top: calc(${coords[1]}px - 12px); width: ${coords[2] - coords[0]}px; height: 10px`" />
                <div class="max-h-[90svh]">
                    <img v-if="imageStore.processedImage"
                         class="rounded-sm object-contain max-h-[90svh] w-full"
                         :src="imageStore.processedImage"
                         @load="imageLoaded" />
                </div>
            </div>
            <template #footer>
                <button @click="download"
                        class="transition-colors bg-green-600 hover:bg-green-900 rounded-md mx-auto mt-2 size-10">
                    <i class="bi bi-download text-2xl"></i>
                </button>
            </template>
        </ModalComponent>
    </main>
</template>
