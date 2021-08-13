import { Component } from '@angular/core';
import { AuthService } from './services/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'libscoutR';
  user = 'Guest';
  isAuthenticated = false;

  constructor(public authService: AuthService) {
    this.authService.isAuthenticated.subscribe(
      (isAuthenticated: boolean) => this.isAuthenticated = isAuthenticated
    );
  }

  async ngOnInit(): Promise<void> {
    this.isAuthenticated = await this.authService.checkAuthenticated();
    this.authService.getUser().then((user:any) => {
      this.user = user.login.substr(0, user.login.indexOf('@'));
    }).catch(err => {
      this.user = 'Guest';
    });
    this.user = 'Loading...'
  }

  async logout(): Promise<void> {
    await this.authService.logout('');
  }

}
