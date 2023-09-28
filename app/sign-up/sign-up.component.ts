import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ValidatorFn, AbstractControl } from '@angular/forms';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss'],
})
export class SignUpComponent implements OnInit {
  signupForm: FormGroup;

  constructor(private fb: FormBuilder, @Inject('AuthService') private authService: AuthService) {
    this.signupForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      firstName: ['', [Validators.required, Validators.minLength(2)]],
      password1: ['', [Validators.required, Validators.minLength(7)]],
      password2: ['', [Validators.required, this.matchPassword()]],
    });
  }

  ngOnInit(): void {
    this.signupForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      firstName: ['', [Validators.required, Validators.minLength(2)]],
      password1: ['', [Validators.required, Validators.minLength(7)]],
      password2: ['', [Validators.required, this.matchPassword()]],
    });
  }

  onSubmit(): void {
    if (this.signupForm.invalid) {
      return;
    }

    this.authService
      .signUp(this.signupForm.value)
      .subscribe(() => {
        // Account created successfully
      });
  }

  matchPassword(): ValidatorFn {
    return (control: AbstractControl): { [key: string]: any } | null => {
      const password1 = control.root.get('password1');
      const password2 = control.value;
      if (password1 && password2 && password1.value !== password2) {
        return { matchPassword: true };
      }
      return null;
    };
  }
}