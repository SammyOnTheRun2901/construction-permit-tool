import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatFormFieldModule,
    MatInputModule,
    MatCheckboxModule,
    MatButtonModule,
    MatTableModule,
    MatIconModule
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  form: FormGroup;
  loading = false;
  error = '';
  results: any[] = [];
  displayedColumns: string[] = ['regulation', 'result', 'notes'];

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.form = this.fb.group({
      country: ['Denmark', Validators.required],
      ceilingHeight: [null, Validators.required],
      handrails: [false],
      fireSafety: [false],
      far: [null, Validators.required],
      parkingSpaces: [null, Validators.required],
      accessibleEntrances: [null, Validators.required]
    });
  }

  submit() {
    this.loading = true;
    this.error = '';
    this.results = [];
    this.http.post<any>('http://localhost:5000/validate', this.form.value).subscribe({
      next: res => {
        this.loading = false;
        if (res.status === 'success') {
          this.results = res.results || [];
        } else {
          this.error = 'Validation failed.';
        }
      },
      error: err => {
        this.loading = false;
        this.error = 'Error connecting to backend.';
      }
    });
  }
}