from django import forms
from .models import userAuth, user, documento, student, proffessor, otherUser

class login(forms.ModelForm):
    class Meta:
        model = userAuth
        fields = ['user', 'password']
        widgets = {
                'user': forms.TextInput(attrs={'class': 'form-control'}),
                'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            }


class signin(forms.ModelForm):
    # Campos adicionales del modelo de autorización
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    
    # Campos adicionales del modelo student
    nombres = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres del estudiante'})
    )
    apellidos = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos del estudiante'})
    )
    cursoId = forms.ModelChoiceField(
        queryset=student.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Curso'
    )
    
    # Campos adicionales del modelo proffessor
    nombresP = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres del profesor'})
    )
    apellidosP = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos del profesor'})
    )

    # Campos adicionales del modelo otherUser
    nombresO = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres de otro'})
    )
    apellidosO = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos de otro'})
    )

    class Meta:
        model = user
        fields = ['correo', 'Cod_identif']
        labels = {
            'correo': 'Correo electrónico',
            'Cod_identif': 'Carné de identificación',
        }
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'Cod_identif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carné de identificación'}),
        }

    def save(self, commit=True):
        # Guardar el modelo `user`
        user_instance = super().save(commit=False)

        if commit:
            user_instance.save()

            # Crear y guardar el modelo `userAuth` relacionado
            user_auth_instance = userAuth(
                id_user=user_instance,
                user=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
            user_auth_instance.save()

            # Verificar el rol seleccionado y guardar los modelos correspondientes
            selected_role = self.data.get('opciones')

            if selected_role == 'estudiante':
                # Crear y guardar el modelo `student` relacionado
                student_instance = student(
                    id_user=user_instance,
                    nombres=self.cleaned_data['nombres'],
                    apellidos=self.cleaned_data['apellidos'],
                    cursoId=self.cleaned_data['cursoId']
                )
                student_instance.save()

            elif selected_role == 'profesor':
                # Crear y guardar el modelo `professor` relacionado
                proffessor_instance = proffessor(
                    id_user=user_instance,
                    nombresP=self.cleaned_data['nombresP'],
                    apellidosP=self.cleaned_data['apellidosP']
                )
                proffessor_instance.save()
            
            elif selected_role == 'otro':
                # Crear y guardar el modelo `otherUser` relacionado
                otherUser_instance = otherUser(
                    id_user=user_instance,
                    nombresO=self.cleaned_data['nombresO'],
                    apellidosO=self.cleaned_data['apellidosO']
                )
                otherUser_instance.save()

        return user_instance


class createAuthentication(forms.ModelForm):
    class Meta:
        model = userAuth
        fields = [
            'user',
            'password'
        ]
        labels = {
            'user': 'Nombre de usuario',
            'password': 'Crea una contraseña'
        }
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Crea una contraseña'})
        }


class upload(forms.ModelForm):
    class Meta:
        model = documento
        fields = [
            'nombreDoc',
            'fechaAprobado',
        ]