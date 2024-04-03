<template>
    <div class="inline-flex items-center">
        <label class="relative flex items-center p-[2px]"
               htmlFor="custom">
            <input type="checkbox"
                   class="peer cursor-pointer relative appearance-none w-5 h-5"
                   id="custom" />
            <span
                  class="absolute text-black text-lg transition-opacity opacity-0 pointer-events-none top-2/4 left-2/4 -translate-y-2/4 -translate-x-2/4 peer-checked:opacity-100">
                <i class="bi bi-check-lg"></i>
            </span>
        </label>
    </div>
</template>
