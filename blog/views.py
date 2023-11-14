from django.shortcuts import render
from django.utils import timezone
from .models import Character,Equipement
from django.shortcuts import render, get_object_or_404,redirect
from .forms import MoveForm

 
# Create your views here.

 
def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    Equip = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)
    else:
        form = MoveForm()
    
    
    if form.is_valid():
        message = ""
        ancien_lieu = Equip

        ancien_lieu.disponibilite = "libre"
        
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)

        if nouveau_lieu.disponibilite == "libre":

            if nouveau_lieu.id_equip =="Piste":
                if character.etat == "Pret":  
                    character.etat = "Vide"
                    character.lieu = nouveau_lieu
                    nouveau_lieu.disponibilite = "occupé"
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas Pret" 
                    return render(request,'blog/character_detail.html',{'message':message})
                
            elif nouveau_lieu.id_equip =="Pompe":
                if character.etat == "Vide":  
                    character.etat = "Panne"
                    character.lieu = nouveau_lieu
                    nouveau_lieu.disponibilite = "occupé"
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas Vide"
                    return render(request,'blog/character_detail.html',{'message':message}) 

            elif nouveau_lieu.id_equip =="Garage":
                if character.etat == "Panne":  
                    character.etat = "Pret"
                    character.lieu = nouveau_lieu
                    ancien_lieu.save()
                    nouveau_lieu.save()
                    character.save()
                else:
                    message = character.id_character + " n'est pas en Panne" 
                    return render(request,'blog/character_detail.html',{'message':message})
        else:
            message= nouveau_lieu.id_equip + " est déja occcupé"
            form = MoveForm()
            return render(request,'blog/character_detail.html',{'message':message})
        
        return redirect('character_detail', id_character=id_character)

    
    else: 
        form = MoveForm()
        return render(request,
                  'blog/character_detail.html',
                  {'character': character, 'lieu': character.lieu, 'form': form,'message':""})



def post_Acceuil(request):
    equip = Equipement.objects.all()
    caractere = Character.objects.all()
    return render(request, 'blog/post_Acceuil.html', {'Character': caractere,'Equipement' : equip})

