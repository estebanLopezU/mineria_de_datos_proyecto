// Interactive 3D Animations and Effects
document.addEventListener('DOMContentLoaded', function() {
    // Add 3D tilt effect to options
    const options = document.querySelectorAll('.option');

    options.forEach(option => {
        option.addEventListener('mouseenter', function(e) {
            this.style.transform = 'perspective(1000px) rotateX(5deg) rotateY(5deg) translateZ(10px)';
            this.style.transition = 'transform 0.3s ease';
        });

        option.addEventListener('mouseleave', function(e) {
            this.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        });
    });

    // Animate checkboxes on check
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (this.checked) {
                label.style.color = '#27ae60';
                label.style.transform = 'scale(1.05)';
                label.style.transition = 'all 0.3s ease';
            } else {
                label.style.color = '';
                label.style.transform = 'scale(1)';
            }
        });
    });

    // Button click animation
    const button = document.querySelector('button');
    button.addEventListener('click', function() {
        this.innerHTML = '<span>Ejecutando...</span>';
        this.style.animation = 'pulse 1s infinite';

        // Reset after 2 seconds
        setTimeout(() => {
            this.innerHTML = 'Ejecutar Optimización';
            this.style.animation = '';
        }, 2000);
    });

    // Disk visualization interaction
    const disk3d = document.querySelector('.disk-3d');
    if (disk3d) {
        disk3d.addEventListener('click', function() {
            this.style.animation = 'rotateY 2s linear';
            setTimeout(() => {
                this.style.animation = 'rotateY 8s infinite linear';
            }, 2000);
        });
    }

    // Add particle effect on load
    createParticles();

    function createParticles() {
        const container = document.querySelector('.container');
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(52, 152, 219, 0.3);
                border-radius: 50%;
                pointer-events: none;
                animation: float ${2 + Math.random() * 3}s ease-in-out infinite;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 2}s;
            `;
            container.appendChild(particle);
        }
    }
});

// Add CSS for additional animations
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    .particle {
        position: absolute;
        pointer-events: none;
    }
`;
document.head.appendChild(style);