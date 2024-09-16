function toggleAdvancedSettings() {
    const advancedSettings = document.getElementById('advanced-settings');
    const toggleButton = document.getElementById('toggle-button');
    if (advancedSettings.classList.contains('hidden')) {
        advancedSettings.classList.remove('hidden');
        toggleButton.textContent = 'Schowaj Zaawansowane Ustawienia';
    } else {
        advancedSettings.classList.add('hidden');
        toggleButton.textContent = 'Pokaż Zaawansowane Ustawienia';
    }
}