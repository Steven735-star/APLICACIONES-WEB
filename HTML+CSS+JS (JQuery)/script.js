$(function(){
  // Responsive navigation
  $('.nav-toggle').on('click',function(){
    const isOpen=$('.main-nav').toggleClass('open').hasClass('open');
    $(this).attr('aria-expanded',isOpen).text(isOpen?'×':'☰');
  });
  $('.main-nav a').on('click',function(){
    $('.main-nav').removeClass('open');
    $('.nav-toggle').attr('aria-expanded','false').text('☰');
  });

  // Workshop requirement: hero button changes background color randomly.
  $('#changeHeroColor').on('click',function(){
    const hue=Math.floor(Math.random()*360);
    const saturation=38+Math.floor(Math.random()*18);
    const lightness=15+Math.floor(Math.random()*7);
    $('.hero').css('background-color',`hsl(${hue} ${saturation}% ${lightness}%)`);
  });

  // Workshop requirement: gallery image opens enlarged in a popup modal.
  function openModal(img){
    const src=$(img).attr('src');
    const alt=$(img).attr('alt');
    const caption=$(img).data('caption')||alt;
    $('#modalImage').attr({src:src,alt:alt});
    $('#modalCaption').text(caption);
    $('#imageModal').addClass('open').attr('aria-hidden','false').hide().fadeIn(180);
    $('body').css('overflow','hidden');
    $('.modal-close').trigger('focus');
  }
  function closeModal(){
    $('#imageModal').fadeOut(160,function(){
      $(this).removeClass('open').attr('aria-hidden','true');
      $('body').css('overflow','');
    });
  }
  $('.gallery-item').on('click',function(){openModal($(this).find('img'));});
  $('.gallery-item').on('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();openModal($(this).find('img'));}});
  $('.modal-close,.modal-backdrop').on('click',closeModal);
  $(document).on('keydown',function(e){if(e.key==='Escape'&&$('#imageModal').hasClass('open'))closeModal();});

  // Optional rating field for clients who want to review the service.
  $('#reason').on('change',function(){
    const showRating=$(this).val()==='rating';
    $('#ratingField').stop(true,true)[showRating?'slideDown':'slideUp'](180).attr('aria-hidden',String(!showRating));
    if(!showRating){$('#rating').val('');$('.stars button').removeClass('active');$('#ratingError').text('');}
  });
  $('.stars button').on('click',function(){
    const value=Number($(this).data('rating'));
    $('#rating').val(value);
    $('.stars button').each(function(){
      $(this).toggleClass('active',Number($(this).data('rating'))<=value);
    });
    $('#ratingError').text('');
  });

  $('#message').on('input',function(){
    if(this.value.length>500)this.value=this.value.slice(0,500);
    $('#charCount').text(`${this.value.length} / 500`);
  });

  function setError(selector,message){
    $(selector).text(message).closest('.field').addClass('invalid');
  }
  function clearErrors(){
    $('.error').text('');
    $('.field').removeClass('invalid');
    $('#formStatus').text('');
  }
  function validEmail(email){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);}

  // Workshop requirement: validate name, email and message before submission.
  $('#contactForm').on('submit',function(e){
    e.preventDefault();
    clearErrors();
    const name=$('#name').val().trim();
    const email=$('#email').val().trim();
    const reason=$('#reason').val();
    const message=$('#message').val().trim();
    const consent=$('#consent').is(':checked');
    const rating=$('#rating').val();
    let valid=true;

    if(name.length<2){setError('#nameError','Ingresa un nombre válido.');valid=false;}
    if(!validEmail(email)){setError('#emailError','Ingresa un correo electrónico válido.');valid=false;}
    if(!reason){setError('#reasonError','Selecciona el motivo de tu mensaje.');valid=false;}
    if(reason==='rating'&&!rating){setError('#ratingError','Selecciona una calificación de 1 a 5 estrellas.');valid=false;}
    if(message.length<10){setError('#messageError','Escribe un mensaje de al menos 10 caracteres.');valid=false;}
    if(!consent){$('#consentError').text('Debes aceptar el uso de los datos para continuar.');valid=false;}

    if(valid){
      alert('Form submitted successfully!');
      $('#formStatus').text('¡Gracias! Tu formulario fue validado correctamente.');
      this.reset();
      $('#charCount').text('0 / 500');
      $('#rating').val('');
      $('.stars button').removeClass('active');
      $('#ratingField').hide().attr('aria-hidden','true');
    }
  });

  $('#year').text(new Date().getFullYear());
});
