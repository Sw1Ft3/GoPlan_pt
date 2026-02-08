/**
 * Управление темами (светлая/темная)
 * Поддерживает автоматическое определение системной темы
 * и сохранение выбора пользователя
 */

(function() {
    'use strict';

    // Определение системной темы
    function getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    // Получение текущей темы
    function getCurrentTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        return getSystemTheme();
    }

    // Применение темы
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        document.body.setAttribute('data-theme', theme);
        
        // Обновление meta тега для браузеров
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', theme === 'dark' ? '#212529' : '#ffffff');
        }
        
        // Сохранение в localStorage
        localStorage.setItem('theme', theme);
        
        // Вызов события для других скриптов
        window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }

    // Обновление иконки темы
    function updateThemeIcon(theme) {
        const themeIcon = document.querySelector('.theme-icon');
        if (themeIcon) {
            themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
            themeIcon.setAttribute('aria-label', theme === 'dark' ? 'Переключить на светлую тему' : 'Переключить на темную тему');
        }
        
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Переключить на светлую тему' : 'Переключить на темную тему');
            themeToggle.setAttribute('title', theme === 'dark' ? 'Переключить на светлую тему' : 'Переключить на темную тему');
        }
    }

    // Переключение темы
    function toggleTheme() {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        applyTheme(newTheme);
        updateThemeIcon(newTheme);
        
        // Анимация переключения
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        
        // Удаление transition после завершения
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    // Инициализация при загрузке DOM
    function initTheme() {
        const theme = getCurrentTheme();
        applyTheme(theme);
        updateThemeIcon(theme);
        
        // Добавление обработчика на кнопку переключения
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', toggleTheme);
            
            // Поддержка клавиатуры
            themeToggle.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleTheme();
                }
            });
        }
        
        // Слушатель изменений системной темы (если пользователь не выбрал тему вручную)
        if (window.matchMedia && !localStorage.getItem('theme')) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            // Современный способ
            if (mediaQuery.addEventListener) {
                mediaQuery.addEventListener('change', function(e) {
                    if (!localStorage.getItem('theme')) {
                        const newTheme = e.matches ? 'dark' : 'light';
                        applyTheme(newTheme);
                        updateThemeIcon(newTheme);
                    }
                });
            } 
            // Старый способ для совместимости
            else if (mediaQuery.addListener) {
                mediaQuery.addListener(function(e) {
                    if (!localStorage.getItem('theme')) {
                        const newTheme = e.matches ? 'dark' : 'light';
                        applyTheme(newTheme);
                        updateThemeIcon(newTheme);
                    }
                });
            }
        }
    }

    // Инициализация при готовности DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }

    // Экспорт функций для глобального доступа (если нужно)
    window.themeManager = {
        toggle: toggleTheme,
        getCurrent: getCurrentTheme,
        setTheme: applyTheme
    };

})();
