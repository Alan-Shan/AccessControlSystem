import {library} from "@fortawesome/fontawesome-svg-core";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {
    faHome,
    faCheck,
    faXmark,
    faPlus,
    faPen,
    faUser,
    faUserEdit,
    faUserMinus,
    faUserPlus,
    faSignInAlt,
    faSignOutAlt,
    faTrash
} from "@fortawesome/free-solid-svg-icons";

// FA icons

library.add(faHome, faUser, faUserPlus, faSignInAlt, faSignOutAlt, faCheck, faXmark, faTrash, faPlus, faUserEdit, faUserMinus,
    faPen);

export {FontAwesomeIcon};