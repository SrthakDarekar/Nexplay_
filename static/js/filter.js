function filterCards(game){

    const cards = document.querySelectorAll('.tournament-card');
    const normalizedGame = game ? game.toLowerCase() : '';

    cards.forEach(card => {
        const cardGame = card.dataset.game ? card.dataset.game.toLowerCase() : '';

        if (normalizedGame === 'all' || normalizedGame === 'all games') {
            card.style.display = 'block';
        } else if (cardGame === normalizedGame) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });

}

