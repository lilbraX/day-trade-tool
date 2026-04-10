import { Nav } from "@/components/nav";
import { APP_NAME } from "@/lib/constants/app";

export default function SettingsPage() {
  return (
    <>
      <Nav />
      <div className="card">
        <h2>Settings</h2>
        <p>App Name: {APP_NAME}</p>
        <form className="grid" style={{ maxWidth: 420 }}>
          <label>Default Fee<input defaultValue="120" /></label>
          <label>Timezone<input defaultValue="Asia/Tokyo" /></label>
          <label>Initial Capital<input defaultValue="1000000" /></label>
          <label>Display Theme<select defaultValue="dark"><option value="dark">dark</option></select></label>
        </form>
      </div>
    </>
  );
}
