const navLinks = document.querySelectorAll('nav a');

const hrefContainsQuestions = (link) => {
    let linkHref = link.href.split('/').slice(0,-1);
    let windowHref= window.location.href.split('/').slice(0,-1);
    
    if (windowHref.join('') === linkHref.join('') && link.href.includes('questions')) {
        return true;
    }
}

const changeLinkAppearance = () => {
    for (let link of navLinks) {
        if (hrefContainsQuestions(link)) {
            link.classList.add('deactivate');
            return;
        }

        if (window.location.href === link.href) {
            link.classList.add('deactivate');
        } else {
            if (link.classList.contains('deactivate') && !hrefContainsQuestions(link)) {
                link.classList.remove('deactivate');
            };
        };
    };
};

changeLinkAppearance();