import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LibrarianLoginComponent } from './components/librarian-login/librarian-login.component';
import { MisplacedBookComponent } from './components/misplaced-book/misplaced-book.component';
import { SearchBookComponent } from './components/search-book/search-book.component';
import { AuthGuardService } from './services/auth-guard/auth-guard.service';

const routes: Routes = [
  {path: 'misplaced', component: MisplacedBookComponent, canActivate: [ AuthGuardService ]},
  {path: 'login', component: LibrarianLoginComponent},
  {path: 'search', component: SearchBookComponent },
  {path: '**', component: LibrarianLoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
