# SinCos Arch – KDE Plasma 6 splash

Teema vastaa sincos.py:n asetuksia luontihetkellä. Myöhemmät Python-muutokset eivät päivity QML-teemaan automaattisesti.

Asenna projektin juuresta (ilman sudoa):

```bash
mkdir -p ~/.local/share/plasma/look-and-feel
cp -r kde-splash/org.sincos.arch ~/.local/share/plasma/look-and-feel/
```

Esikatsele ikkunassa:

```bash
ksplashqml --test --window org.sincos.arch
```

Valitse Järjestelmäasetuksista Aloitusruutu / Splash Screen ja teemaksi SinCos Arch. Käytä asetusten hakua löytääksesi sivun. Tämä ruutu näkyy kirjautumisen jälkeen Plasman käynnistyessä.

Muokkaa asennetun teeman contents/splash/Splash.qml-tiedoston vakioita. centerSpinSpeed on nyt 0; esimerkiksi 90 pyörittää keskikuvaa 90 astetta sekunnissa. centerPulsePeriod määrittää koko kutistumis- ja kasvusyklin sekunteina.

Kuvan voi vaihtaa tiedostosta contents/splash/images/arch.png.

Varmennus: qmllint onnistui, ja ksplashqml latasi teeman offscreen-tilassa ilman QML-virheitä. Graafinen esikatselu ja oikea kirjautuminen tulee tarkistaa KDE-istunnossa.
