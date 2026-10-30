(function () {
  'use strict';

  var form = document.getElementById('vehicule-form');
  if (!form) { return; }

  var button = document.getElementById('submit-btn');
  var MIN_YEAR = 1980;
  var MAX_YEAR = new Date().getFullYear() + 1;
  var MAX_PRICE = 999999999;

  function setError(id, message) {
    var input = document.getElementById(id);
    var box = document.getElementById('err-' + id);
    if (!input || !box) { return; }
    box.textContent = message;
    if (message) {
      input.setAttribute('aria-invalid', 'true');
    } else {
      input.removeAttribute('aria-invalid');
    }
  }

  function validate() {
    var firstInvalid = null;

    function fail(id, message) {
      setError(id, message);
      if (!firstInvalid) { firstInvalid = document.getElementById(id); }
    }

    ['marque', 'modele'].forEach(function (id) {
      var value = document.getElementById(id).value.trim();
      setError(id, '');
      if (!value) {
        fail(id, 'Ce champ est obligatoire.');
      } else if (value.length > 50) {
        fail(id, 'Maximum 50 caractères.');
      }
    });

    var yearRaw = document.getElementById('annee').value.trim();
    setError('annee', '');
    if (yearRaw !== '') {
      var year = Number(yearRaw);
      if (!Number.isInteger(year) || year < MIN_YEAR || year > MAX_YEAR) {
        fail('annee', 'Entrez une année entre ' + MIN_YEAR + ' et ' + MAX_YEAR + '.');
      }
    }

    var priceRaw = document.getElementById('prix').value.trim();
    setError('prix', '');
    if (priceRaw !== '') {
      var price = Number(priceRaw);
      if (!isFinite(price) || price < 0 || price > MAX_PRICE) {
        fail('prix', 'Entrez un prix positif.');
      }
    }

    if (firstInvalid) { firstInvalid.focus(); }
    return !firstInvalid;
  }

  function resetButton() {
    button.disabled = false;
    button.textContent = button.getAttribute('data-label');
  }

  form.addEventListener('submit', function (event) {
    if (!validate()) {
      event.preventDefault();
      return;
    }

    if (document.getElementById('prevenir_clients').checked &&
        !window.confirm('Un message va être envoyé à tous les clients. Continuer ?')) {
      event.preventDefault();
      return;
    }

    button.disabled = true;
    button.textContent = 'Envoi en cours...';
  });

  // Retour arrière du navigateur : on rend le bouton utilisable à nouveau.
  window.addEventListener('pageshow', resetButton);
})();